#!/usr/bin/env sh
set -eu

SECURITY_DIR=/opt/geoserver_data/security
DEV_SECURITY_DIR=/opt/dev-security

if [ -n "${GEOSERVER_REQUIRE_FILE:-}" ] && [ ! -f "$GEOSERVER_REQUIRE_FILE" ]; then
  echo "Initialize $GEOSERVER_DATA_DIR from data directory included in geoserver.war"
  cp -r "$CATALINA_HOME/webapps/geoserver/data"/* "$GEOSERVER_DATA_DIR"
fi

mkdir -p "$SECURITY_DIR/role/default" "$SECURITY_DIR/usergroup/default"
chown -R geoserver:geoserver "$SECURITY_DIR"

cp "$DEV_SECURITY_DIR/layers.properties" "$SECURITY_DIR/layers.properties"
cp "$DEV_SECURITY_DIR/role/default/roles.xml" "$SECURITY_DIR/role/default/roles.xml"
cp "$DEV_SECURITY_DIR/usergroup/default/users.xml" "$SECURITY_DIR/usergroup/default/users.xml"

chown geoserver:geoserver \
  "$SECURITY_DIR/layers.properties" \
  "$SECURITY_DIR/role/default/roles.xml" \
  "$SECURITY_DIR/usergroup/default/users.xml"

exec runuser -u geoserver -- "$CATALINA_HOME/bin/catalina.sh" run
