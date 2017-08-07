
1. URL mapping

General Routing concept etween Polymer and Flask is being described here:
https://wmginsberg.github.io/blog/poly-flask

See below the implemented mapping rules on the back-end side

'Upload' Blueprint
<Rule '/upload/pulse/visualizations' (HEAD, POST, OPTIONS, GET) -> upload.add_visualization>,
<Rule '/upload/pulse/visualizations' (HEAD, POST, OPTIONS, GET) -> add_visualization>,
<Rule '/upload/pulse/dashboards' (HEAD, POST, OPTIONS, GET) -> add_photos>,
<Rule '/upload/static/<filename>' (HEAD, OPTIONS, GET) -> upload.static>,
<Rule '/files/<uuid>' (HEAD, OPTIONS, GET) -> upload_complete>
<Rule '/add/upload' (POST, OPTIONS) -> add_upload>,

'Visualization API' Blueprint
<Rule '/api/pulse/visualizations' (HEAD, OPTIONS, GET) -> get_visualizations_api>,
<Rule '/api/pulse/visualizations' (POST, OPTIONS) -> post_visualization_api>,
<Rule '/api/pulse/visualizations/<name>' (HEAD, OPTIONS, GET) -> get_visualization_api>,
<Rule '/api/pulse/visualizations/<name>' (OPTIONS, DELETE) -> delete_visualization_api>,

'Dashboard API' Blueprint
<Rule '/api/pulse/dashboards' (HEAD, OPTIONS, GET) -> get_dashboards_api>,
<Rule '/api/pulse/dashboards' (POST, OPTIONS) -> post_dashboard_api>,
<Rule '/api/pulse/dashboards/<name>' (HEAD, OPTIONS, GET) -> get_dashboard_api>,
<Rule '/api/pulse/dashboards/<name>' (OPTIONS, DELETE) -> delete_dashboard_api>,

'Visualization' Blueprint
<Rule '/pulse/visualizations' (HEAD, OPTIONS, GET) -> get_visualization_list>,
<Rule '/pulse/visualizations/<name>' (HEAD, OPTIONS, GET) -> get_visualization>,

'Dashboard' Blueprint
<Rule '/pulse/dashboards' (HEAD, OPTIONS, GET) -> get_dashboard_list>,
<Rule '/pulse/dashboards/<name>' (HEAD, OPTIONS, GET) -> get_dashboard>,


<Rule '/register' (HEAD, POST, OPTIONS, GET) -> security.register>,
<Rule '/logout' (HEAD, OPTIONS, GET) -> security.logout>,
<Rule '/login' (HEAD, POST, OPTIONS, GET) -> security.login>,
<Rule '/lost' (HEAD, OPTIONS, GET) -> lost>,
<Rule '/add' (HEAD, OPTIONS, GET) -> index>,
<Rule '/' (HEAD, OPTIONS, GET) -> home>,
<Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,


2. Goal is to empower user to share visualizations and templates with self-provisioning. Dashboard will be covered later.

    - Visualizations (basic view with static files, form, model..)
    - Templates (basic view with static files, model & form - TBD). Changes to take real template definition as an input.
    - Dashboards (too much html customization.. not yet eligible for self-provisioning)

3. Todo

    - Change polymer element view based on current user (admin vs editor vs reader)
    - update the template API / Form to enable self-provisioning from the template export
    - safety control process to follow before making the new templates & visualizations available to public users
    - registration with email notification

4. Usage

    - Start MongoDB (update settings.py file to change db settings)
    - run 'run-dev' script with python 2.7