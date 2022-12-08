from google.cloud import monitoring_v3
from google.protobuf import field_mask_pb2 as field_mask
import os

def save_notification_channels_in_ather_policy(event, context):
    try:
        project_id = os.environ.get('project_id', None)
        if project_id == None:
            project_id = os.environ["GCP_PROJECT"]
    except:
        print(
            "Please use Python version 3.7 or select environment variable \'key\' project_id and \'value\' your project id")
        return
    try:
        alert_id_main = os.environ.get('alert_id_main', "None")
        alert_id_backup = os.environ.get('alert_id_backup', "None")
        if alert_id_main == "None" or alert_id_backup == "None":
            print("please select alert ids")
            return
    except:
        print("please select alert ids")
        return

    change = False
    name = "projects/" + project_id + "/alertPolicies/"
    client = monitoring_v3.AlertPolicyServiceClient()
    policy_main = client.get_alert_policy(name = name + alert_id_main)
    policy_backup = client.get_alert_policy(name = name + alert_id_backup)

    if policy_main.notification_channels:
        policy_backup.notification_channels.clear()
        for notify in policy_main.notification_channels:
            policy_backup.notification_channels.append(notify)
        policy_main.notification_channels.clear()
        change = True
    else:
        if policy_backup.notification_channels:
            for notify in policy_backup.notification_channels:
                policy_main.notification_channels.append(notify)
        else:
            print("backup alert is empty")
            return
        
    mask = field_mask.FieldMask()
    mask.paths.append("notification_channels")
    client.update_alert_policy(alert_policy=policy_main, update_mask=mask)
    client.update_alert_policy(alert_policy=policy_backup, update_mask=mask)
    print("Notification Channels Updated" if not change else "Notification Channels Clear", policy_main.name)
    if change:
        print("Notification Channels Updated", policy_backup.name)