from flask import Flask, render_template, request, url_for, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

from Backend.DataClasses.StatusWniosku import StatusWniosku
from app import app, db

from Models.tables import Klienci, Uzytkownicy, Adresy, KlienciIndywidualni, Firmy


