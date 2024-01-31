from flask import Blueprint, flash, redirect, render_template, current_app, request, url_for
from flask_login import LoginManager, login_required, logout_user, current_user, login_user

from app.utilities.video_utils import *
from app.utilities.file_system_utils import *

from app.extensions.plotly_pose_data import plotly_pose_figure
from app.extensions.plotly_pose_contact_points import plotly_pose_contact_points

import json
import pandas as pd
import plotly
import pytz
import random

bp = Blueprint("dictionary", __name__, url_prefix="/dictionary")
tz = pytz.timezone('UTC')


@bp.route('/search', methods=['GET'])
def pose_search():
    title = "Explore Pole Shapes"
    data = pd.read_csv(os.path.join(
        'app', 'static', 'dictionary', 'tricks', 'pose_data.csv'))
    pose_names = data['pose_name'].unique()
    total_poses = len(pose_names)
    query = request.args.get('q', '')
    filepath_src = 'dictionary/tricks/'
    if query:
        filtered_data = data[data['pose_name'].str.contains(
            query, case=False, na=False)]
        results = filtered_data.to_dict(orient='records')
    else:
        results = data.sample(n=5, random_state=random.randint(
            1, len(data))).to_dict(orient='records')

    return render_template("dictionary/tricks/search.html", results=results, title=title, pose_names=pose_names, total_poses=total_poses, filepath_src=filepath_src)


@bp.route('/detail/<pose_name>', methods=['GET'])
def pose_detail_page(pose_name):
    if_spine = request.args.get('spine', 'true').lower() == 'true'
    if_right_arm = request.args.get('right_arm', 'false').lower() == 'true'
    if_left_arm = request.args.get('left_arm', 'false').lower() == 'true'
    if_right_leg = request.args.get('right_leg', 'false').lower() == 'true'
    if_left_leg = request.args.get('left_leg', 'false').lower() == 'true'
    data = pd.read_csv(os.path.join(
        'app', 'static', 'dictionary', 'tricks', 'pose_data.csv'))
    filtered_data = data[data['pose_name'] == pose_name]
    image_filename = 'dictionary/tricks/' + \
        filtered_data['image_filename'].values[0]
    fig = plotly_pose_figure(filtered_data, 0, spine=if_spine, right_arm=if_right_arm,
                             left_arm=if_left_arm, right_leg=if_right_leg, left_leg=if_left_leg)
    fig_plot = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("dictionary/tricks/detail_plot_figure.html", fig_plot=fig_plot, title=pose_name, image_filename=image_filename)


@bp.route('/detail/<pose_name>/points', methods=['GET'])
def pose_detail_contact_points(pose_name):
    data = pd.read_csv(os.path.join(
        'app', 'static', 'dictionary', 'tricks', 'pose_data.csv'))
    filtered_data = data[data['pose_name'] == pose_name]
    image_filename = 'dictionary/tricks/' + \
        filtered_data['image_filename'].values[0]
    fig = plotly_pose_contact_points(filtered_data, 0)
    fig_plot = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("dictionary/tricks/detail_plot_contacts.html", fig_plot=fig_plot, title=pose_name, image_filename=image_filename)


@bp.route('/search/legs', methods=['GET'])
def pose_legs_search():
    title = "Explore Leg Positions"
    data = pd.read_csv(os.path.join(
        'app', 'static', 'dictionary', 'positions', 'legs', 'pose_data.csv'))
    pose_names = data['pose_name'].unique()
    total_poses = len(pose_names)
    query = request.args.get('q', '')
    filepath_src = 'dictionary/positions/legs/'
    if query:
        filtered_data = data[data['pose_name'].str.contains(
            query, case=False, na=False)]
        results = filtered_data.to_dict(orient='records')
    else:
        results = data.sample(n=5, random_state=random.randint(
            1, len(data))).to_dict(orient='records')
    return render_template("dictionary/legs/search.html", results=results, title=title, pose_names=pose_names,
                           total_poses=total_poses, filepath_src=filepath_src)


@bp.route('/detail/legs/<pose_name>', methods=['GET'])
def pose_legs_detail_page(pose_name):
    if_spine = request.args.get('spine', 'false').lower() == 'true'
    if_right_arm = request.args.get('right_arm', 'false').lower() == 'true'
    if_left_arm = request.args.get('left_arm', 'false').lower() == 'true'
    if_right_leg = request.args.get('right_leg', 'true').lower() == 'true'
    if_left_leg = request.args.get('left_leg', 'true').lower() == 'true'
    data = pd.read_csv(os.path.join(
        'app', 'static', 'dictionary', 'positions', 'legs', 'pose_data.csv'))
    filtered_data = data[data['pose_name'] == pose_name]
    image_filename = 'dictionary/positions/legs/' + \
        filtered_data['image_filename'].values[0]
    fig = plotly_pose_figure(filtered_data, 0, spine=if_spine, right_arm=if_right_arm,
                             left_arm=if_left_arm, right_leg=if_right_leg, left_leg=if_left_leg)
    fig_plot = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("dictionary/legs/detail_plot_figure.html", fig_plot=fig_plot, title=pose_name, image_filename=image_filename)


@bp.route('/detail/legs/<pose_name>/points', methods=['GET'])
def pose_legs_detail_contact_points(pose_name):
    data = pd.read_csv(os.path.join(
        'app', 'static', 'dictionary', 'positions', 'legs', 'pose_data.csv'))
    filtered_data = data[data['pose_name'] == pose_name]
    image_filename = 'dictionary/positions/legs/' + \
        filtered_data['image_filename'].values[0]
    fig = plotly_pose_contact_points(filtered_data, 0)
    fig_plot = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("dictionary/legs/detail_plot_contacts.html", fig_plot=fig_plot, title=pose_name, image_filename=image_filename)

@bp.route('/search/grip', methods=['GET'])
def pose_grip_search():
    title = "Explore Grip Positions"
    data = pd.read_csv(os.path.join('app', 'static', 'dictionary', 'positions', 'grip', 'pose_data.csv'))
    data = data[~data['pose_name'].str.contains('-inv')]
    pose_names = data['pose_name'].unique()
    total_poses = len(pose_names)
    query = request.args.get('q', '')
    filepath_src = 'dictionary/positions/grip/'
    if query:
        filtered_data = data[data['pose_name'].str.contains(query, case=False, na=False)]
        filtered_data = filtered_data[~filtered_data['pose_name'].str.contains('-inv')]
        results = filtered_data.to_dict(orient='records')
    else:
        results = data.sample(n=5, random_state=random.randint(
            1, len(data))).to_dict(orient='records')
    return render_template("dictionary/grip/search.html", results=results, title=title, pose_names=pose_names,
                           total_poses=total_poses, filepath_src=filepath_src)


@bp.route('/detail/grip/<pose_name>', methods=['GET'])
def pose_grip_detail_page(pose_name):
    if_spine = request.args.get('spine', 'false').lower() == 'true'
    if_right_arm = request.args.get('right_arm', 'true').lower() == 'true'
    if_left_arm = request.args.get('left_arm', 'true').lower() == 'true'
    if_right_leg = request.args.get('right_leg', 'false').lower() == 'true'
    if_left_leg = request.args.get('left_leg', 'false').lower() == 'true'
    data = pd.read_csv(os.path.join(
        'app', 'static', 'dictionary', 'positions', 'grip', 'pose_data.csv'))
    filtered_data = data[~data['pose_name'].str.contains('-inv')]
    image_filename = 'dictionary/positions/grip/' + \
        filtered_data['image_filename'].values[0]
    fig = plotly_pose_figure(filtered_data, 0, spine=if_spine, right_arm=if_right_arm,
                             left_arm=if_left_arm, right_leg=if_right_leg, left_leg=if_left_leg)
    fig_plot = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("dictionary/grip/detail_plot_figure.html", fig_plot=fig_plot, title=pose_name, image_filename=image_filename)


@bp.route('/detail/grip/<pose_name>/points', methods=['GET'])
def pose_grip_detail_contact_points(pose_name):
    data = pd.read_csv(os.path.join(
        'app', 'static', 'dictionary', 'positions', 'grip', 'pose_data.csv'))
    filtered_data = data[~data['pose_name'].str.contains('-inv')]
    image_filename = 'dictionary/positions/grip/' + \
        filtered_data['image_filename'].values[0]
    fig = plotly_pose_contact_points(filtered_data, 0)
    fig_plot = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("dictionary/grip/detail_plot_contacts.html", fig_plot=fig_plot, title=pose_name, image_filename=image_filename)
