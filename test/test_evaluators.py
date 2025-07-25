from sqlalchemy import insert
from my_proof.evaluators import ParameterEvaluator
from my_proof.models import users


def test_ownership(conn, config):
    evaluator = ParameterEvaluator(config, conn, "")
    result = evaluator.ownership("1@e.com")
    assert result == 1

    conn.execute(insert(users).values(violations=5, email="2@e.com"))
    result = evaluator.ownership("2@e.com", violation_threshold=5)
    assert result == 0


def test_uniqueness(conn, config):
    evaluator = ParameterEvaluator(config, conn, "test/data/1.ogg")
    result = evaluator.uniqueness()
    assert result == 1

    evaluator = ParameterEvaluator(config, conn, "test/data/1.ogg")
    result = evaluator.uniqueness()
    assert result == 0

    evaluator = ParameterEvaluator(config, conn, "test/data/2.ogg")
    result = evaluator.uniqueness()
    assert result == 1

    # Same as 1.ogg
    evaluator = ParameterEvaluator(config, conn, "test/data/3.ogg")
    result = evaluator.uniqueness()
    assert result == 0
