#!bin/bash

conda activate metron

if [[ $(poetry config virtualenvs.create) == "true" ]]
then
  poetry_metron_env_path=$(poetry env list --full-path)
  if [[ $(echo $poetry_metron_env_path | grep Activated) ]]
  then
    source "$( echo $poetry_metron_env_path | grep Activated | cut -d' ' -f1 )/bin/activate"
  else
    source "$( echo $poetry_metron_env_path )/bin/activate"
  fi
fi