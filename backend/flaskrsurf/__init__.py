import os, sys
from flask import Flask, request, jsonify, abort
from models import setup_db, SurfSpot, Surfer, SurfContest
# TODO: from .auth.auth import AuthError, requires_auth
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)


    # ROUTES

    ## PUBLIC GET API
    ''' The default GET API's for any public user'''

    ### GET SURFERS
    @app.route('/surfers', methods=['GET'])
    def get_surfers():
        try:
            surfers_resp = []
            surfers = Surfer.query.order_by(Surfer.id).all()
            for surfer in surfers:
                surfers_resp.append(surfer.format())
            return jsonify({
                "success": True,
                "surfers": surfers_resp
            })

        except:
            abort(400)

    @app.route('/surfers/<int:surfer_id>', methods=['GET'])
    def get_surfer(surfer_id):
        try:
            surfer = Surfer.query.get(surfer_id)
            if surfer is None:
                # TODO: abort in 2 places, how to prevent?
                abort(404)

            return jsonify({
                "success": True,
                "surfer_info": surfer.format()
            })

        except:
            abort(404)

    ### GET SURF SPOTS
    @app.route('/surf_spots', methods=['GET'])
    def get_surf_spots():
        try:
            surfspot_resp = []
            surfspots = SurfSpot.query.order_by(SurfSpot.id).all()
            for surfspot in surfspots:
                print(surfspot.name)
                surfspot_resp.append(surfspot.format())
            return jsonify({
                "success": True,
                "surf_spots": surfspot_resp
            })

        except:
            abort(400)

    ### GET SURF Contests
    @app.route('/surf_contests', methods=['GET'])
    def get_all_surf_contests():
        try:
            surfcontests_resp = []
            surfcontests = SurfContest.query.order_by(SurfContest.id).all()
            for contest in surfcontests:
                surfcontests_resp.append(contest.format())
            return jsonify({
                "success": True,
                "surf_contests": surfcontests_resp
            })

        except:
            abort(400)

    ### GET specific SURF Contests
    @app.route('/surf_contests/<int:contest_id>')
    def get_surf_contest(contest_id):
        try:
            contest = SurfContest.query.get(contest_id)

            if not contest:
                abort(404)

            return jsonify({
                "success": True,
                "surf_contest": contest.format()
            })
        except:
            # TODO: throw better error
            return jsonify({
                "success": False,
                "message": "Could not get contest"
            })


    ### GET specific SURF Contests hosted at a specific spot
    @app.route('/surf_spots/<int:spot_id>/contests', methods=['GET'])
    def get_surf_spot_contests(spot_id):
        try:
            surfSpot = SurfSpot.query.get(spot_id)

            if not surfSpot:
                abort(404)

            contest_resp = []
            contests = surfSpot.contests

            for contest in contests:
                contest_resp.append(contest.format())

            return jsonify({
                "success": True,
                "surf_spot": surfSpot.format(),
                "surf_contests": contest_resp
            })

        except:
            # TODO: 404?
            abort(400)


    ### POST to search for specific Surfers
    @app.route('/surfers/search', methods=['POST'])
    def search_surfers():
        body = request.get_json()
        surferSearchTerm = body['search_term'].lower()
        searchTerm = "%{}%".format(surferSearchTerm)
        error = False
        surferSearchResults = []
        try:
            surfers = Surfer.query.filter(Surfer.name.ilike(searchTerm)).all()
            for surfer in surfers:
                surferSearchResults.append(surfer.format())

            return jsonify({
                "success": True,
                "count": len(surfers),
                "surfers": surferSearchResults
            })
        except:
            error = True

    ## RESTRICTED ACCESS API
    ''' The GET/PATCH/POST/DELETE API's for Surf Coordinator users'''

    # POST route for Creating Surf Contests
    @app.route('/surf_contest/create', methods=['POST'])
    def create_surf_contest():
        createError = False
        errorDescr = ''
        try:
            body = request.get_json()
            surfSpotId = body['surf_spot_id']
            contestName = body['contest_name']
            contestDate = body['contest_date']
            contestImage = body['contest_image']

            # Find the surf spot this contest will be held at
            surfSpot = SurfSpot.query.get(surfSpotId)
            if surfSpot == None:
                errorDescr += 'Surf Spot not found. '
                createError = True

            if not createError:
                print(surfSpot.name)
                newContest = SurfContest(
                    name=contestName,
                    date=contestDate,
                    image=contestImage,
                    spotId=surfSpotId)

                newContest.insert()

                surfContests = SurfContest.query.order_by(SurfContest.id).all()
                listSurfContests = []

                for contest in surfContests:
                    listSurfContests.append(contest.format())

                return jsonify({
                    "success": True,
                    "contest_count": len(surfContests),
                    "surf_contests": listSurfContests
                })
        except:
            print(sys.exc_info())
            error = True
            errorDescr = "Error creating new Surf Contest"

        # TODO: Return error code here instead
        return jsonify({
            "success": False,
            "message": errorDescr
        })

    # DELETE route for removing (Cancelling/Postponing) Surf Contests
    @app.route('/surf_contests/<int:contest_id>', methods=['DELETE'])
    def delete_surf_contest(contest_id):
        print("Trying to delete")
        print(contest_id)
        try:
            surfContest = SurfContest.query.get(contest_id)
            if surfContest is not None:
                # Delete this contest
                print("Deleting...")
                surfContest.delete()
                print("Deleted...")

                surfContests = SurfContest.query.order_by(SurfContest.id).all()
                listSurfContests = []

                for contest in surfContests:
                    listSurfContests.append(contest.format())

                return jsonify({
                    "success": True,
                    "contest_count": len(surfContests),
                    "surf_contests": listSurfContests
                })
        except:
            print(sys.exc_info())
            error = True

    return app

app = create_app()

if __name__ == '__main__':
    app.run()