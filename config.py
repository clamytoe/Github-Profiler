#!/usr/bin/env python3
import os


class Config:
    """
    Common configurations
    Put any configurations here that are common across all environments
    """

    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    API_BASE = 'https://api.github.com/users/'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    SQLALCHEMY_ECHO = False
    SECRET_KEY = "FakeK3y"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///gh-profiles.sqlite'


class TestingConfig(Config):
    """
    Testing configurations
    """
    TESTING = True


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False

app_config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
        }
