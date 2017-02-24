# Copyright (c) 2016 Till Mobile Inc.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

FROM ubuntu:14.04
MAINTAINER Till Mobile <n.crafford@tillmobile.com>
RUN echo "#!/bin/sh\nexit 0" > /usr/sbin/policy-rc.d
RUN sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN sudo apt-get update
RUN sudo apt-get -qq -y install wget
RUN sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
RUN sudo apt-get update && sudo apt-get install -y python-pip build-essential tcl8.5 postgresql-9.5 postgresql-contrib-9.5 postgresql-server-dev-9.5 python-dev
RUN sudo pip install virtualenv
RUN sudo sed -e '90d' -i /etc/postgresql/9.5/main/pg_hba.conf
RUN sudo sed -e '91d' -i /etc/postgresql/9.5/main/pg_hba.conf
RUN sudo echo "host all all 0.0.0.0/0 trust" >> '/etc/postgresql/9.5/main/pg_hba.conf'
RUN sudo echo "local all all trust" >> '/etc/postgresql/9.5/main/pg_hba.conf'
RUN sudo sed -e "s/[#]\?listen_addresses = .*/listen_addresses = '*'/g" -i '/etc/postgresql/9.5/main/postgresql.conf'

USER root
RUN chmod 777 /opt/ 
ADD . /opt/
RUN chmod -R 777 /opt/ 
RUN ./opt/test/scripts/bootstrap.sh