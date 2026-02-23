from flask import (
    send_from_directory,
)
from . import main
from app.utils.decorators import *
from app.utils.authorizer import Authorizer


@main.route("/test", methods=["GET"])
@login_required
def test():
    if request.args.get("2"):
        return render_template("policy_center.html")
    return render_template("test.html")


@main.route("/", methods=["GET"])
@login_required
def home():
    return render_template("home.html")

@main.route("/integrations", methods=["GET"])
@login_required
def integrations():
    return render_template("integrations.html")

@main.route("/projects/<string:pid>/reports/<path:filename>", methods=["GET"])
@login_required
def download_report(pid, filename):
    result = Authorizer(current_user).can_user_access_project(pid)
    return send_from_directory(
        directory=current_app.config["UPLOAD_FOLDER"], path=filename, as_attachment=True
    )


@main.route("/frameworks", methods=["GET"])
@login_required
def frameworks():
    return render_template("frameworks.html")


@main.route("/tenants/<string:id>/risk", methods=["GET"])
@login_required
def risks(id):
    Authorizer(current_user).can_user_access_risk_module(id)
    return render_template("risk_register.html")


@main.route("/policies", methods=["GET"])
@login_required
def policies():
    return render_template("policies.html")


@main.route("/tenants/<string:id>/policy-center", methods=["GET"])
@login_required
def view_policy_center(id):
    Authorizer(current_user).can_user_access_tenant(id)
    policy_id = request.args.get("policy-id")
    return render_template("pc.html", tenant_id=id, policy_id=policy_id)


@main.route("/projects", methods=["GET"])
@login_required
def projects():
    return render_template("projects.html")


@main.route("/projects/<string:pid>", methods=["GET"])
@login_required
def view_project(pid):
    result = Authorizer(current_user).can_user_access_project(pid)
    return render_template("view_project.html", project=result["extra"]["project"])


@main.route("/projects/<string:pid>/controls/<string:cid>", methods=["GET"])
@login_required
def view_control_in_project(pid, cid):
    result = Authorizer(current_user).can_user_read_project_control(cid)
    return render_template(
        "view_control_in_project.html",
        project=result["extra"]["control"].project,
        project_control=result["extra"]["control"],
    )


@main.route("/projects/<string:id>/policy-center", methods=["GET"])
@login_required
def view_policy_center_for_project(id):
    result = Authorizer(current_user).can_user_read_project(id)
    policy_id = request.args.get("policy-id")
    return render_template(
        "policy_center.html", project=result["extra"]["project"], policy_id=policy_id
    )


@main.route("/labels", methods=["GET"])
@login_required
def labels():
    return render_template("labels.html")


@main.route("/tags", methods=["GET"])
@login_required
def tags():
    return render_template("tags.html")


@main.route("/vendors/<string:id>", methods=["GET"])
@login_required
def get_vendor(id):
    result = Authorizer(current_user).can_user_access_vendor(id)
    vendor = result["extra"]["vendor"]
    return render_template("view_vendor.html", vendor=vendor)


@main.route("/applications/<string:id>", methods=["GET"])
@login_required
def get_application(id):
    result = Authorizer(current_user).can_user_access_application(id)
    application = result["extra"]["application"]
    return render_template("view_application.html", application=application)


@main.route("/search-vendors", methods=["GET"])
@login_required
def search_vendor():
    # TODO - auth
    return render_template("search_vendor.html")
