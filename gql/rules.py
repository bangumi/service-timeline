from typing import Dict, Tuple

from ariadne.contrib.tracing.utils import is_introspection_key
from graphql import (
    ASTValidationRule,
    DefinitionNode,
    FieldNode,
    FragmentDefinitionNode,
    FragmentSpreadNode,
    GraphQLError,
    InlineFragmentNode,
    Node,
    OperationDefinitionNode,
    ValidationContext,
)
from graphql.validation.validate import ValidationAbortedError


def depth_limit_validator(max_depth: int):
    class DepthLimitValidator(ASTValidationRule):
        def __init__(self, validation_context: ValidationContext):
            document = validation_context.document
            definitions = document.definitions

            fragments = get_fragments(definitions)
            queries = get_queries_and_mutations(definitions)
            query_depths = {}

            for name in queries:
                query_depths[name] = determine_depth(
                    node=queries[name],
                    fragments=fragments,
                    depth_so_far=0,
                    max_depth=max_depth,
                    context=validation_context,
                    operation_name=name,
                )
            super().__init__(validation_context)

    return DepthLimitValidator


def get_fragments(
    definitions: Tuple[DefinitionNode, ...],
) -> Dict[str, FragmentDefinitionNode]:
    fragments = {}
    for definition in definitions:
        if isinstance(definition, FragmentDefinitionNode):
            fragments[definition.name.value] = definition
    return fragments


def get_queries_and_mutations(
    definitions: Tuple[DefinitionNode, ...],
) -> Dict[str, OperationDefinitionNode]:
    operations = {}

    for definition in definitions:
        if isinstance(definition, OperationDefinitionNode):
            operation = definition.name.value if definition.name else "anonymous"
            operations[operation] = definition
    return operations


def determine_depth(
    node: Node,
    fragments: Dict[str, FragmentDefinitionNode],
    depth_so_far: int,
    max_depth: int,
    context: ValidationContext,
    operation_name: str,
) -> int:
    if depth_so_far > max_depth:
        context.report_error(
            GraphQLError(
                f"'{operation_name}' exceeds maximum operation depth of {max_depth}.",
                [node],
            )
        )
        raise ValidationAbortedError
    if isinstance(node, FieldNode):
        should_ignore = is_introspection_key(node.name.value)

        if should_ignore or not node.selection_set:
            return 0
        return 1 + max(
            determine_depth(
                node=selection,
                fragments=fragments,
                depth_so_far=depth_so_far + 1,
                max_depth=max_depth,
                context=context,
                operation_name=operation_name,
            )
            for selection in node.selection_set.selections
        )
    if isinstance(node, FragmentSpreadNode):
        return determine_depth(
            node=fragments[node.name.value],
            fragments=fragments,
            depth_so_far=depth_so_far,
            max_depth=max_depth,
            context=context,
            operation_name=operation_name,
        )
    if isinstance(
        node, (InlineFragmentNode, FragmentDefinitionNode, OperationDefinitionNode)
    ):
        return max(
            determine_depth(
                node=selection,
                fragments=fragments,
                depth_so_far=depth_so_far,
                max_depth=max_depth,
                context=context,
                operation_name=operation_name,
            )
            for selection in node.selection_set.selections
        )
    raise Exception(f"Depth crawler cannot handle: {node.kind}.")  # pragma: no cover
