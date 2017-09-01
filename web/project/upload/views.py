from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, send_from_directory
import glob, os, json
import errno
from project.visualizations.forms import AddVisualizationForm
from project.templates.forms import AddTemplateForm
from project.utils.uploadsets import upload_jar_plugins, upload_images, \
    upload_exported_templates, upload_exported_options
from flask_security import login_required, auth_token_required, current_user
from project.models import Visualizations, Templates
from flask_principal import Permission, RoleNeed


blueprint = Blueprint('upload', __name__, url_prefix='/pulse/upload', static_url_path='/assets', static_folder='assets/user', template_folder='templates')

# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))
editor_permission = Permission(RoleNeed('editor'))


@blueprint.route('/visualizations', methods=['GET', 'POST'])
@login_required
#@admin_permission.require(http_exception=403)
def add_visualization():

    form = AddVisualizationForm()

#    if form.validate_on_submit(): # to get error messages to the browser

    if request.method == 'POST' and 'vis_image' in request.files:
        filename1 = upload_images.save(request.files['vis_image'], current_user.email)
        filename2 = upload_images.save(request.files['vis_options'], current_user.email)
        filename3 = upload_jar_plugins.save(request.files['vis_manifest'], current_user.email)

        name = "{}-{}".format(form.vis_title.data.replace(" ", ""), current_user.email)

        image_src = "{}{}/screenshots/{}".format(blueprint.url_prefix, blueprint.static_url_path, filename1)
        image_src = image_src[1:]

        image_edit = "{}{}/screenshots/{}".format(blueprint.url_prefix, blueprint.static_url_path, filename2)
        image_edit = image_edit[1:]

        plugin_src = "{}{}/plugins/{}".format(blueprint.url_prefix, blueprint.static_url_path, filename3)
        plugin_src = plugin_src[1:]

        viz =Visualizations(title=form.vis_title.data, name=name, short_desc=form.vis_short_desc.data,
                            desc=form.vis_desc.data, rating=form.vis_rating.data, contributor=current_user.email,
                            image_src=image_src, image_edit=image_edit, plugin_src=plugin_src)

        viz.save()

        #return redirect(url_for('upload.complete', user_email=current_user.email))
        return redirect(url_for('visualizations.get_visualization_list'))


    return render_template('upload/add_visualization.html', form=form)


@blueprint.route('/templates', methods=['GET', 'POST'])
@login_required
#@admin_permission.require(http_exception=403)
def add_template():

    form = AddTemplateForm()

    if request.method == 'POST' and 'template_export' in request.files and 'ss_options_export' in request.files:

        filename1 = upload_exported_templates.save(request.files['template_export'], current_user.email)

        if request.files['template_image'].filename == '':
            print "No available screenshot"
            image_src = ''
        else:
            filename2 = upload_images.save(request.files['template_image'], current_user.email)
            image_src = "{}{}/screenshots/{}".format(blueprint.url_prefix, blueprint.static_url_path, filename2)
            image_src = image_src[1:]

        filename3 = upload_exported_options.save(request.files['ss_options_export'], current_user.email)

        template_src = "{}{}/definitions/{}".format(blueprint.url_prefix, blueprint.static_url_path, filename1)
        template_src = template_src[1:]

        template_src_file = "{}/definitions/{}".format(blueprint.static_folder, filename1)

        ss_option_src = "{}{}/options/{}".format(blueprint.url_prefix, blueprint.static_url_path, filename3)
        ss_option_src = ss_option_src[1:]


        with open(template_src_file) as fh:
            tmp = json.load(fh)
            if 'definition' in tmp:
                definition = tmp['definition']
                name = definition['guid']
            elif 'template' in tmp:
                definition = tmp['template'][0]['definition']
                name = definition['guid']
            else:
                print 'Template definition not accurate'
                name = None

        metadata = {'image_src':image_src, 'contributor':current_user.email,
                    'template_src':template_src, 'ss_option_src':ss_option_src}

        template = Templates(name=name, definition=definition, rating=form.template_rating.data, metadata=metadata)

        template.save()

        return redirect(url_for('templates.get_template_list'))
        #return redirect(url_for('upload.complete', user_email=current_user.email))

    return render_template('upload/add_template.html', form=form)



'''
# Route that will process the file upload
@blueprint.route('/', methods=['GET','POST'])
@login_required
def upload():
    form = request.form
    if request.method == 'POST':
        target = "{}/users/{}".format(blueprint.root_path, current_user.email)
        try:
            os.mkdir(target)
        except OSError as e:
            if e.errno == errno.EEXIST:
                print("Couldn't create directory {}".format(target))

        for upload in request.files.getlist("file"):
            filename = upload.filename.rsplit("/")[0]
            destination = '/'.join([target, filename])
            print( "Accepting: {}\n and saving to: {}".format(filename, destination))
            upload.save(destination)

        return redirect(url_for('upload.complete', user_email=current_user.email))
    return render_template('upload/post.html', form=form)
'''


@blueprint.route("/files/<user_email>", methods=['GET', 'POST'])
def complete(user_email):
    location = "{}/assets/user/screenshots/{}".format(blueprint.root_path, user_email)

    if not os.path.isdir(location):
        return "Error! {} not found!".format(location)

    print url_for('static', filename='test/')
    print url_for('upload.static', filename='test/')

    files = []
    for file in glob.glob("{}/*.*".format(location)):
        fname = file.split(os.sep)[-1]
        files.append(fname)

    return render_template('upload/complete.html', user_email=user_email, files=files)
