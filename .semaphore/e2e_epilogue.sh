artifact push job "$PROJECT_DIR"/django_server.log
artifact push job "$FRONTEND_DIR"/vue_server.log
artifact push job "$FRONTEND_DIR"/cypress/videos
SCREENSHOTS_DIR="$FRONTEND_DIR"/cypress/screenshots
if [ -d "$SCREENSHOTS_DIR" ]; then
  artifact push job "$SCREENSHOTS_DIR";
fi;
artifact push job "$FRONTEND_DIR"/cypress/logs
test-results publish cypress/results/report.xml
