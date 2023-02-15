FROM xiaoqianxiao/test:latest

LABEL maintainer="xiaoqian@stanford.edu"

# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
WORKDIR ${FLYWHEEL}

# Save docker environ
ENV PYTHONUNBUFFERED 1
# Dev install. git for pip editable install.
RUN apt-get update && apt-get install -y --no-install-recommends git && \
    pip install --no-cache "poetry==1.1.10"

# Installing main dependencies
COPY pyproject.toml poetry.lock $FLYWHEEL/
RUN poetry install --no-dev

############## DEV ONLY ##########
#COPY user.json /root/.config/flywheel/user.json
# Copy executable/manifest to Gear
COPY manifest.json ${FLYWHEEL}/manifest.json
COPY fw_gear_precurate ${FLYWHEEL}/fw_gear_precurate
COPY run.py ${FLYWHEEL}/run.py

# Configure entrypoint
RUN chmod a+x ${FLYWHEEL}/run.py
ENTRYPOINT ["poetry","run","python","/flywheel/v0/run.py"]
