from flask import Blueprint, request, jsonify, g
from models.user import User
from schemas.user import UserSchema
from schemas.likes import LikeSchema
from schemas.dislike import DislikeSchema
from schemas.match import MatchSchema
from app import db
from lib.secure_route import secure_route
from marshmallow import ValidationError
from models.likes import Like
from models.dislikes import Dislike
from models.matches import Match

user_schema = UserSchema()
like_schema = LikeSchema()
dislike_schema = DislikeSchema()
match_schema = MatchSchema()
# GET all users
router = Blueprint(__name__, 'users')
@router.route('/users', methods=['GET'])
@secure_route
def get_users():
  users = User.query.all()
  print('hello')
  return user_schema.jsonify(users, many=True), 200
@router.route('/likes', methods=['GET', 'POST'])
@secure_route
def like():
  like_data = request.get_json()
  like_instance = Like(
    liker_id=g.current_user.id,
    liked_id=like_data['liked_id']
  )
  like_instance.save()
  likers_of_user=Like.query.filter_by(liked_id=g.current_user.id, liker_id=like_data['liked_id']).first()
  if not likers_of_user: 
    return like_schema.jsonify(like_data)
  else:
    match = Match(
      user_1_id=likers_of_user.liked_id,
      user_2_id=likers_of_user.liker_id
    )
    match.save()
    return "Match"
@router.route('/dislikes', methods=['POST'])
@secure_route
def dislike():
  dislike_data = request.get_json()
  dislike_instance = Dislike(
    disliker_id=g.current_user.id,
    disliked_id=dislike_data['disliked_id']
  )
  print(dislike_instance)
  dislike_instance.save()
  return dislike_schema.jsonify(dislike_data)

@router.route('/seen', methods=['POST'])
@secure_route
def post_seen():
  seen_data = request.get_json()
  existing_user = User.query.get(g.current_user.id)
  if not existing_user.has_seen:
    existing_user.has_seen = [seen_data['id']]
  else:
    existing_user.has_seen = existing_user.has_seen + [seen_data['id']]
  existing_user.save()
  # seen_instance = User(
  #   has_seen = has_seen.append(seen_data)

  return user_schema.jsonify(existing_user)














