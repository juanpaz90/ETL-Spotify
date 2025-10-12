#!/bin/bash

install_packages() {
  pip install pipenv
  pipenv install
}

install_packages
