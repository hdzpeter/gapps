from flask import (
    jsonify,
    request
)
from . import api
from app.utils.decorators import login_required
from app.utils.integrations import api_get, api_post, api_put, api_delete


# -------------------------
# Integration Endpoints
# -------------------------

@api.route("/integrations", methods=["GET"])
@login_required
def list_integrations():
    response = api_get("integrations")
    return jsonify(response)

@api.route("/integrations/<string:id>", methods=["GET"])
@login_required
def get_integration(id):
    response = api_get(f"integrations/{id}")
    return jsonify(response)

@api.route("/integrations", methods=["POST"])
@login_required
def create_integration():
    data = request.get_json()
    response = api_post("integrations", payload=data)
    return jsonify(response)

# -------------------------
# Deployment Endpoints
# -------------------------

@api.route("/deployments", methods=["GET"])
@login_required
def list_deployments():
    response = api_get("deployments")
    return jsonify(response)


@api.route("/deployments", methods=["POST"])
@login_required
def create_deployment():
    data = request.get_json()
    response = api_post("deployments", payload=data)
    return jsonify(response)


@api.route("/deployments/<deployment_id>", methods=["PUT"])
@login_required
def update_deployment(deployment_id):
    data = request.get_json()
    response = api_put(f"deployments/{deployment_id}", data)
    return jsonify(response)

@api.route("/deployments/<string:id>", methods=["GET"])
@login_required
def get_deployment(id):
    response = api_get(f"deployments/{id}")
    return jsonify(response)

@api.route("/deployments/<string:id>", methods=["DELETE"])
@login_required
def delete_deployment(id):
    response = api_delete(f"deployments/{id}")
    return jsonify(response)

@api.route("/deployments/scheduled", methods=["GET"])
@login_required
def get_scheduled_deployments():
    response = api_get("api/deployments/scheduled")
    return jsonify(response)


@api.route("/deployments/<string:id>/violations", methods=["GET"])
@login_required
def list_violations_for_deployment(id):
    response = api_get(f"deployments/{id}/violations")
    return jsonify(response)


# -------------------------
# Job Endpoints
# -------------------------

@api.route("/jobs", methods=["GET"])
@login_required
def list_jobs():
    # Get pagination parameters from the request
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    # Pass them to the backend API
    response = api_get(f"jobs?page={page}&per_page={per_page}")
    return jsonify(response)


@api.route("/jobs/<string:job_id>", methods=["GET"])
@login_required
def get_job(job_id):
    response = api_get(f"jobs/{job_id}")
    return jsonify(response)

@api.route("/deployments/<string:deployment_id>/jobs", methods=["POST", "GET"])
@login_required
def execute_manual_deployment(deployment_id):
    response = api_get(f"deployments/{deployment_id}")

    if response.get("schedule"):
        return jsonify({"message": "deployment is not manual"})

    data = {"deployment_id": deployment_id}
    response = api_post(f"jobs", data)
    return jsonify(response)

@api.route("/init-integrations", methods=["POST","GET"])
@login_required
def deploy_integrations():
    response = api_post(f"init-integrations")
    return jsonify(response)

# -------------------------
# Violation Endpoints
# -------------------------

@api.route("/violations", methods=["GET"])
@login_required
def list_violations():
    response = api_get("violations")
    return jsonify(response)