from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from .gpt import AssistantAPI
import logging

logger = logging.getLogger(__name__)
bp = Blueprint('frontend', __name__, url_prefix='/')

@bp.route('/index',methods=['GET'])
def index():
    return render_template('index.html')