
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):

    __tablename__ = "students"

    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    career_path = db.Column(db.String(50))
    mathematical_level = db.Column(db.Float)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    # unit_progress = db.relationship('UnitProgress', back_populates='unit')

    # unit_progress = db.relationship('Unit', back_populates='student')
    concept_progress = db.relationship('Concept', back_populates='student')
    problem_progress = db.relationship('Student', back_populates='student')


    def __repr__(self):
        return f"<Student student_id={self.student_id} email={self.email}>"

class Unit(db.Model):

    __tablename__ = "units"

    unit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    level_req = db.Column(db.Float)

    # unit_progress = db.relationship('UnitProgress', back_populates='unit')
    concepts = db.relationship('Concept', back_populates='unit')

    def __repr__(self):
        return f"<Unit unit_id={self.unit_id}>"

class Concept(db.Model):

    __tablename__ = "concepts"

    concept_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'))
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.goal_id'))

    concept_progress = db.relationship('ConceptProgress', back_populates='concept')
    goal = db.relationship('Goal', back_populates='concept')
    unit = db.relationship('Unit', back_populates='concepts')


    def __repr__(self):
        return f"<Concept concept_id={self.concept_id}>"

class Problem(db.Model):

    __tablename__ = "problems"

    problem_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    point_worth = db.Column(db.Integer)
    concept_id = db.Column(db.Integer)

    problem_progress = db.relationship('ProblemProgress', back_populates='problem')

    def __repr__(self):
        return f"<Problem problem_id={self.problem_id}>"


class UnitProgress(db.Model):

    __tablename__ = "units_complete"

    units_done = db.Column(db.String(100))
    units_completion = db.Column(db.Boolean, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'))


    student = db.relationship('Student', back_populates='unit_progress')
    unit = db.relationship('Unit', back_populates='unit_progress')

    def __repr__(self):
        return f"<UnitProgress completion={self.Units_completion}>"


class ConceptProgress(db.Model):

    __tablename__ = "concepts_complete"

    concepts_done = db.Column(db.String(100))
    concepts_completion = db.Column(db.Boolean, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    concept_id = db.Column(db.Integer, db.ForeignKey('concepts.concept_id'))

    student = db.relationship('Student', back_populates='concept_progress')
    concept = db.relationship('Concept', back_populates='concept_progress')


    def __repr__(self):
        return f"<ConceptProgress completion={self.concepts_completion}>"

class ProblemProgress(db.Model):

    __tablename__ = "problems_complete"

    problems_done = db.Column(db.String(100))
    problems_completion = db.Column(db.Boolean, primary_key=True)
    points_gained = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.problem_id'))

    student = db.relationship('Student', back_populates='problem_progress')
    problem = db.relationship('Problem', back_populates='problem_progress')


    def __repr__(self):
        return f"<ProblemProgress problem_id={self.problems_completion}>"

class Goal(db.Model):

    __tablename__ = "goals"

    goal_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    r_w_apps = db.Column(db.String(100))

    concept = db.relationship('Concept', back_populates='goal')

    def __repr__(self):
        return f"<Goal goal_id={self.goal_id}>"


class UnitEquation(db.Model):

    __tablename__ = "unit_equations"

    unit_equation_set = db.Column(db.String(100), primary_key=True)
    equation_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)

    def __repr__(self):
        return f"<UnitEquation equation_id={self.equation_id}>"

class ConceptEquation(db.Model):

    __tablename__ = "concept_equations"

    concept_equation_set = db.Column(db.String(100), primary_key=True)
    concept_id = db.Column(db.Integer)
    equation_id = db.Column(db.Integer)

    def __repr__(self):
        return f"<ConceptEquation equation_id={self.equation_id}>"

class ProblemEquation(db.Model):

    __tablename__ = "problem_equations"

    problem_equation_set = db.Column(db.String(100), primary_key=True)
    problem_id = db.Column(db.Integer)
    equation_id = db.Column(db.String)

    def __repr__(self):
        return f"<ProblemEquation equation_id={self.equation_id}>"

class UserInput(db.Model):

    __tablename__ = "user_inputs"

    user_input_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    problem_id = db.Column(db.Integer)
    all_inputs = db.Column(db.String)

    def __repr__(self):
        return f"<UserInput user_input_id={self.user_input_id}>"

class Equation(db.Model):

    __tablename__ = "equations"

    equation_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    equation = db.Column(db.String(100))

    def __repr__(self):
        return f"<Equation equation_id={self.equation_id}>"

class MathExpression(db.Model):

    __tablename__ = "math_expressions"

    expression_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    problem_id = db.Column(db.Integer)

    def __repr__(self):
        return f"<MathExpression expression_id={self.expression_id}>"


def connect_to_db(flask_app, db_uri="postgresql:///ratings", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)
    db.create_all()
    print("Connected to the db!")

if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)
    connect_to_db(app)
