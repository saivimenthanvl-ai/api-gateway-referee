import pytest
from app.scoring import ScoringEngine
@pytest.fixture
def scoring_engine():
    return ScoringEngine()
def test_basic_analysis(scoring_engine):
    result = scoring_engine.analyze(
        rps=100,
        budget=500,
        latency=100,
        features=["rate_limiting", "auth"],
        use_case="rest",
        weights={
            "cost": 25,
            "latency": 30,
            "features": 20,
            "ops": 15,
            "lockin": 10
        }
    )
    
    assert "winner" in result
    assert "breakdown" in result
    assert len(result["breakdown"]) == 3
    assert "apigateway" in result["breakdown"]
    assert "alb" in result["breakdown"]
    assert "nlb" in result["breakdown"]


def test_high_latency_requirement(scoring_engine):
    result = scoring_engine.analyze(
        rps=100,
        budget=500,
        latency=5,  # Very strict latency
        features=[],
        use_case="rest",
        weights={
            "cost": 10,
            "latency": 60,  # Latency is priority
            "features": 5,
            "ops": 15,
            "lockin": 10
        }
    )
    
    # NLB should score highest on latency
    assert result["breakdown"]["nlb"]["latency"] > result["breakdown"]["alb"]["latency"]
    assert result["breakdown"]["nlb"]["latency"] > result["breakdown"]["apigateway"]["latency"]


def test_many_features_required(scoring_engine):
    result = scoring_engine.analyze(
        rps=100,
        budget=1000,
        latency=100,
        features=["rate_limiting", "auth", "caching", "waf"],
        use_case="rest",
        weights={
            "cost": 10,
            "latency": 10,
            "features": 60,  # Features are priority
            "ops": 15,
            "lockin": 5
        }
    )
    
    # API Gateway should score highest on features
    assert result["breakdown"]["apigateway"]["features"] > result["breakdown"]["alb"]["features"]
    assert result["breakdown"]["apigateway"]["features"] > result["breakdown"]["nlb"]["features"]


def test_cost_scores_inverse(scoring_engine):
    costs = {"apigateway": 200, "alb": 50, "nlb": 40}
    budget = 500
    
    cost_scores = scoring_engine.calculate_cost_scores(costs, budget)
    
    # Lower cost should have higher score
    assert cost_scores["nlb"] > cost_scores["alb"]
    assert cost_scores["alb"] > cost_scores["apigateway"]


def test_feature_scores_empty_features(scoring_engine):
    """Test feature scoring with no required features"""
    feature_scores = scoring_engine.calculate_feature_scores([])
    
    # All should have perfect score if no features required
    assert feature_scores["apigateway"] == 100
    assert feature_scores["alb"] == 100
    assert feature_scores["nlb"] == 100


def test_sensitivity_analysis(scoring_engine):
    result = scoring_engine.analyze_sensitivity(
        rps=100,
        budget=500,
        latency=100,
        features=["rate_limiting"],
        use_case="rest",
        current_weights={
            "cost": 25,
            "latency": 30,
            "features": 20,
            "ops": 15,
            "lockin": 10
        }
    )
    
    assert "base_winner" in result
    assert "flip_points" in result
    assert isinstance(result["flip_points"], list)


def test_extreme_rps(scoring_engine):
    result = scoring_engine.analyze(
        rps=10000,
        budget=5000,
        latency=100,
        features=[],
        use_case="rest",
        weights={
            "cost": 25,
            "latency": 30,
            "features": 20,
            "ops": 15,
            "lockin": 10
        }
    )
    
    # Should still return valid results
    assert result["winner"] in ["apigateway", "alb", "nlb"]
    assert all(0 <= result["breakdown"][opt]["total"] <= 100 
              for opt in ["apigateway", "alb", "nlb"])


def test_zero_budget_edge_case(scoring_engine):
    result = scoring_engine.analyze(
        rps=10,
        budget=10,  # Very low budget
        latency=100,
        features=[],
        use_case="rest",
        weights={
            "cost": 50,  # Cost is critical
            "latency": 20,
            "features": 10,
            "ops": 10,
            "lockin": 10
        }
    )
    
    # Should prefer cheapest option
    assert result["breakdown"]["nlb"]["cost"] >= result["breakdown"]["alb"]["cost"]