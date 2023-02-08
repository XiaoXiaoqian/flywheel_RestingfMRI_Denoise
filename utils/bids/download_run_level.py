def download_bids_for_runlevel(
    hierarchy,
    destination_id,
    output_dir):
    """Copy fmriprep processed output to working container.
    Args:
        hierarchy: the dictionary of the run level info
        destination_id: id of the destination of the gear
    """
    group_label = 'nolanw'
    project_label = hierarchy['project_label']
    subject = hierarchy['subject_label']
    session = hierarchy['session_label']
    acquisition = hierarchy['acquisition_label']
    run_level = hierarchy["run_level"]
    project_finder = 'group=' + group_label + ',label=' + project_label
    project = client.projects.find_one(project_finder)
    #run_level is in ["project", "subject", "session", "acquisition"]
    if run_level == 'project':
        sessions = project.sessions()
        for s in sessions:   
            sub_name = s.subject.label
            prep_list = []
            createdTime_list = []
            if sub_name.startswith(sub_of_interest):
                analyses = s.reload()['analyses']
                session_name = s.label
                for a in analyses:
                    if a.gear_info:
                        if (a.gear_info.name == file_of_interest and a.files):
                            analysisID =  a._id
                            prep_list.append(a._id)
                            createdTime_list.append(a.created.strftime("%Y-%m-%d"))
                if len(prep_list) > 1:
                    latest_index = createdTime_list.index(max(createdTime_list))
                    analysisID = prep_list[latest_index]
                if prep_list:
                    print('start download sub-' + sub_name + '_session-' + session_name)
                    analysis = client.get(analysisID)
                    for f in analysis.files:
                        if f.name.startswith(file_of_interest):
                            output_file_name = os.path.join(output_dir,'fmriprep/zip_files',f.name)
                            if not os.path.exists(output_file_name):
                                   f.download(output_file_name)
    else:
        destination_id = gtk_context.destination["id"]
        destination = client.get(destination_id)
        analyses = s.reload()['analyses']
        prep_list = []
        createdTime_list = []
        for a in analyses:
            if a.gear_info:
                if (a.gear_info.name == file_of_interest and a.files):
                    analysisID =  a._id
                    prep_list.append(a._id)
                    createdTime_list.append(a.created.strftime("%Y-%m-%d"))
            if len(prep_list) > 1:
                latest_index = createdTime_list.index(max(createdTime_list))
                analysisID = prep_list[latest_index]
            if prep_list:
                analysis = client.get(analysisID)
                for f in analysis.files:
                    if f.name.startswith(file_of_interest):
                        output_file_name = os.path.join(output_dir,'fmriprep/zip_files',f.name)
                        if not os.path.exists(output_file_name):
                               f.download(output_file_name)
                            
def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]