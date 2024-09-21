from chii.db.sa import sync_session_maker
from chii.db.tables import ChiiSubject


def test_subject_get():
    SessionMaker = sync_session_maker()
    with SessionMaker() as session:
        s = session.get(ChiiSubject, 333707)
        assert s.name == "Love, Death & Robots Volume 3"
