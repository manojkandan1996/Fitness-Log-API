from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug.exceptions import BadRequest, NotFound

app = Flask(__name__)
api = Api(app)

workouts = []
workout_id_counter = 1

class WorkoutListResource(Resource):
    def get(self):
        return {'workouts': workouts}, 200

    def post(self):
        global workout_id_counter
        data = request.get_json()

        if not data or 'user' not in data or 'type' not in data or 'duration' not in data:
            raise BadRequest("User, type, and duration are required.")

        try:
            duration = float(data['duration'])
            if duration <= 0:
                raise ValueError
        except ValueError:
            raise BadRequest("Duration must be a number greater than 0.")

        new_workout = {
            'id': workout_id_counter,
            'user': data['user'],
            'type': data['type'],
            'duration': duration
        }
        workouts.append(new_workout)
        workout_id_counter += 1
        return new_workout, 201

class WorkoutResource(Resource):
    def get(self, id):
        workout = next((w for w in workouts if w['id'] == id), None)
        if not workout:
            raise NotFound("Workout not found.")
        return workout, 200

    def put(self, id):
        data = request.get_json()
        workout = next((w for w in workouts if w['id'] == id), None)
        if not workout:
            raise NotFound("Workout not found.")

        if 'user' in data:
            workout['user'] = data['user']
        if 'type' in data:
            workout['type'] = data['type']
        if 'duration' in data:
            try:
                duration = float(data['duration'])
                if duration <= 0:
                    raise ValueError
                workout['duration'] = duration
            except ValueError:
                raise BadRequest("Duration must be a number greater than 0.")

        return workout, 200

    def delete(self, id):
        global workouts
        workout = next((w for w in workouts if w['id'] == id), None)
        if not workout:
            raise NotFound("Workout not found.")
        workouts = [w for w in workouts if w['id'] != id]
        return {'message': f'Workout with id {id} deleted.'}, 200

class WorkoutSummaryResource(Resource):
    def get(self):
        total_duration = sum(w['duration'] for w in workouts)
        return {'total_duration': total_duration}, 200

# Register resources
api.add_resource(WorkoutListResource, '/workouts')
api.add_resource(WorkoutResource, '/workouts/<int:id>')
api.add_resource(WorkoutSummaryResource, '/summary')

if __name__ == '__main__':
    app.run(debug=True)
