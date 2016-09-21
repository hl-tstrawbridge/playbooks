import phantom.rules as phantom
import json
from datetime import datetime, timedelta

##############################
# Start - Global Code Block

""" This playbook executes multiple investigative actions to determine if an ip is malicious. """
import ipaddress
def ipfilter(ip):
    ranges =  ['192.168.0.0/24',]
    for item in ranges:
        if phantom.is_ip(ip) and ipaddress.ip_address(unicode(ip)) not in ipaddress.ip_network(unicode(item)):
            return ip
    return None

# End - Global Code block
##############################

def on_start(container):
    
    # call 'decision_2' block
    decision_2(container=container)

    return

def decision_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["domain_reputation_2:action_result.data.*.Webutation domain info.Safety score", "<", 100],
        ])

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        run_query_2(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)
        whois_domain_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)
        hunt_domain_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return

def decision_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):

    # collect filtered artifact ids for 'if' condition 1
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.sourceAddress', 'artifact:*.id'])
    for container_item in container_data:
        if ipfilter(container_item[0]):
            ip_reputation_1(container=container)
            reverse_ip_2(container=container)
        else:
            Send_Email_safe(container=container)

    return

def reverse_ip_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):

    # collect data for 'reverse_ip_2' call
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.sourceAddress', 'artifact:*.id'])

    parameters = []
    
    # build parameters list for 'reverse_ip_2' call
    for container_item in container_data:
        if container_item[0]:
            parameters.append({
                'ip': container_item[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': container_item[1]},
            })

    if parameters:
        phantom.act("reverse ip", parameters=parameters, assets=['domaintools'], callback=domain_reputation_2, name="reverse_ip_2")    
    else:
        phantom.error("'reverse_ip_2' will not be executed due to lack of parameters")
    
    return

def run_query_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'run_query_2' call
    filtered_results_data_1 = phantom.collect2(container=container, datapath=["domain_reputation_2:filtered-action_result.parameter.domain", "domain_reputation_2:filtered-action_result.parameter.context.artifact_id"], action_results=filtered_results)

    parameters = []
    
    # build parameters list for 'run_query_2' call
    for filtered_results_item_1 in filtered_results_data_1:
        if filtered_results_item_1[0]:
            parameters.append({
                'query': filtered_results_item_1[0],
                'display': "",
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': filtered_results_item_1[1]},
            })

    if parameters:
        phantom.act("run query", parameters=parameters, assets=['splunk_entr'], callback=join_Send_Email_bad_domain, name="run_query_2")    
    else:
        phantom.error("'run_query_2' will not be executed due to lack of parameters")
    
    return

def whois_domain_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'whois_domain_1' call
    filtered_results_data_1 = phantom.collect2(container=container, datapath=["domain_reputation_2:filtered-action_result.parameter.domain", "domain_reputation_2:filtered-action_result.parameter.context.artifact_id"], action_results=filtered_results)

    parameters = []
    
    # build parameters list for 'whois_domain_1' call
    for filtered_results_item_1 in filtered_results_data_1:
        if filtered_results_item_1[0]:
            parameters.append({
                'domain': filtered_results_item_1[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': filtered_results_item_1[1]},
            })

    if parameters:
        phantom.act("whois domain", parameters=parameters, assets=['domaintools'], callback=join_Send_Email_bad_domain, name="whois_domain_1")    
    else:
        phantom.error("'whois_domain_1' will not be executed due to lack of parameters")
    
    return

def Escalate_Domain(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    #Set the status to high and leave the container open
    phantom.update(container, {"severity":"high"})
    
    return

def hunt_domain_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'hunt_domain_1' call
    filtered_results_data_1 = phantom.collect2(container=container, datapath=["domain_reputation_2:filtered-action_result.parameter.domain", "domain_reputation_2:filtered-action_result.parameter.context.artifact_id"], action_results=filtered_results)

    parameters = []
    
    # build parameters list for 'hunt_domain_1' call
    for filtered_results_item_1 in filtered_results_data_1:
        if filtered_results_item_1[0]:
            parameters.append({
                'domain': filtered_results_item_1[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': filtered_results_item_1[1]},
            })

    if parameters:
        phantom.act("hunt domain", parameters=parameters, assets=['isightpartners'], callback=join_Send_Email_bad_domain, name="hunt_domain_1")    
    else:
        phantom.error("'hunt_domain_1' will not be executed due to lack of parameters")
    
    return

def hunt_ip_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'hunt_ip_1' call
    filtered_results_data_1 = phantom.collect2(container=container, datapath=["ip_reputation_1:filtered-action_result.parameter.ip", "ip_reputation_1:filtered-action_result.parameter.context.artifact_id"], action_results=filtered_results)

    parameters = []
    
    # build parameters list for 'hunt_ip_1' call
    for filtered_results_item_1 in filtered_results_data_1:
        if filtered_results_item_1[0]:
            parameters.append({
                'ip': filtered_results_item_1[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': filtered_results_item_1[1]},
            })

    if parameters:
        phantom.act("hunt ip", parameters=parameters, assets=['isightpartners'], callback=join_Send_Email_bad_ip, name="hunt_ip_1")    
    else:
        phantom.error("'hunt_ip_1' will not be executed due to lack of parameters")
    
    return

def domain_reputation_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'domain_reputation_2' call
    inputs_data_1 = phantom.collect2(container=container, datapath=['reverse_ip_2:artifact:*.cef.deviceDnsDomain', 'reverse_ip_2:artifact:*.id'], action_results=results)

    parameters = []
    
    # build parameters list for 'domain_reputation_2' call
    for inputs_item_1 in inputs_data_1:
        if inputs_item_1[0]:
            for domain in inputs_item_1[0]:
                if domain:
                    parameters.append({
                    'domain': domain,
                    # context (artifact id) is added to associate results with the artifact
                    'context': {'artifact_id': inputs_item_1[1]},
                    })

    if parameters:
        phantom.act("domain reputation", parameters=parameters, assets=['virustotal_private'], callback=domain_reputation_2_callback, name="domain_reputation_2", parent_action=action)    
    else:
        phantom.error("'domain_reputation_2' will not be executed due to lack of parameters")
    
    return

##- special functions for domain_reputation_2

def domain_reputation_2_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    decision_3(action=action, success=success, container=container, results=results, handle=handle)
    join_decision_4(action=action, success=success, container=container, results=results, handle=handle)

    return

def decision_4(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["ip_reputation_1:action_result.summary.detected_urls", "==", 0],
            ["domain_reputation_2:action_result.data.*.Webutation domain info.Safety score", "==", 100],
        ],
        logical_operator='and')

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        join_Send_Email_safe(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return

##- special functions for decision_4

def join_decision_4(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    # check if all connected incoming actions are done i.e. have succeeded or failed
    if phantom.actions_done([ 'ip_reputation_1','domain_reputation_2' ]):

        # call connected block "decision_4"
        decision_4(container=container, handle=handle)
    
    return

def Send_Email_safe(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'Send_Email_safe' call

    parameters = []
    
    # build parameters list for 'Send_Email_safe' call
    parameters.append({
        'body': "A safe port scan was detected, see Phantom for details.",
        'to': "michael@phantom.us",
        'from': "admin@phantom.us",
        'attachments': "",
        'subject': "Port Scan determined safe",
    })

    if parameters:
        phantom.act("send email", parameters=parameters, assets=['smtp'], callback=Close, name="Send_Email_safe")    
    else:
        phantom.error("'Send_Email_safe' will not be executed due to lack of parameters")
    
    return

##- special functions for Send_Email_safe

def join_Send_Email_safe(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    # check if all connected incoming actions are done i.e. have succeeded or failed
    if phantom.actions_done([ 'ip_reputation_1','domain_reputation_2' ]):

        # call connected block "Send_Email_safe"
        Send_Email_safe(container=container, handle=handle)
    
    return

def Close(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    #Set the status to low and close the container
    phantom.update(container, {"severity":"low", "status":"resolved"})
    
    return

def Send_Email_bad_domain(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'Send_Email_bad_domain' call

    parameters = []
    
    # build parameters list for 'Send_Email_bad_domain' call
    parameters.append({
        'body': "Check phantom to see output results for bad port scan.",
        'to': "michael@phantom.us",
        'from': "admin@phantom.us",
        'attachments': "",
        'subject': "Port Scan detected from bad domain",
    })

    if parameters:
        phantom.act("send email", parameters=parameters, assets=['smtp'], callback=Escalate_Domain, name="Send_Email_bad_domain")    
    else:
        phantom.error("'Send_Email_bad_domain' will not be executed due to lack of parameters")
    
    return

##- special functions for Send_Email_bad_domain

def join_Send_Email_bad_domain(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    # check if all connected incoming actions are done i.e. have succeeded or failed
    if phantom.actions_done([ 'run_query_2','whois_domain_1','hunt_domain_1' ]):

        # call connected block "Send_Email_bad_domain"
        Send_Email_bad_domain(container=container, handle=handle)
    
    return

def Send_Email_bad_ip(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'Send_Email_bad_ip' call

    parameters = []
    
    # build parameters list for 'Send_Email_bad_ip' call
    parameters.append({
        'body': "Check phantom to see output results for bad port scan.",
        'to': "michael@phantom.us",
        'from': "admin@phantom.us",
        'attachments': "",
        'subject': "Port Scan detected from bad IP",
    })

    if parameters:
        phantom.act("send email", parameters=parameters, assets=['smtp'], callback=Escalate_IP, name="Send_Email_bad_ip")    
    else:
        phantom.error("'Send_Email_bad_ip' will not be executed due to lack of parameters")
    
    return

##- special functions for Send_Email_bad_ip

def join_Send_Email_bad_ip(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    # check if all connected incoming actions are done i.e. have succeeded or failed
    if phantom.actions_done([ 'hunt_ip_1','run_query_1','whois_ip_3' ]):

        # call connected block "Send_Email_bad_ip"
        Send_Email_bad_ip(container=container, handle=handle)
    
    return

def Escalate_IP(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    #Set the status to high and leave the container open
    phantom.update(container, {"severity":"high"})
    
    return

def ip_reputation_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):

    # collect data for 'ip_reputation_1' call
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.sourceAddress', 'artifact:*.id'])

    parameters = []
    
    # build parameters list for 'ip_reputation_1' call
    for container_item in container_data:
        if container_item[0]:
            parameters.append({
                'ip': container_item[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': container_item[1]},
            })

    if parameters:
        phantom.act("ip reputation", parameters=parameters, assets=['virustotal_private'], callback=ip_reputation_1_callback, name="ip_reputation_1")    
    else:
        phantom.error("'ip_reputation_1' will not be executed due to lack of parameters")
    
    return

##- special functions for ip_reputation_1

def ip_reputation_1_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    decision_1(container=container)
    join_decision_4(container=container)

    return

def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["ip_reputation_1:action_result.summary.detected_urls", ">", 0],
        ])

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        run_query_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)
        hunt_ip_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)
        whois_ip_3(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return

def whois_ip_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'whois_ip_3' call
    filtered_results_data_1 = phantom.collect2(container=container, datapath=["ip_reputation_1:filtered-action_result.parameter.ip", "ip_reputation_1:filtered-action_result.parameter.context.artifact_id"], action_results=filtered_results)

    parameters = []
    
    # build parameters list for 'whois_ip_3' call
    for filtered_results_item_1 in filtered_results_data_1:
        if filtered_results_item_1[0]:
            parameters.append({
                'ip': filtered_results_item_1[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': filtered_results_item_1[1]},
            })

    if parameters:
        phantom.act("whois ip", parameters=parameters, assets=['domaintools'], callback=join_Send_Email_bad_ip, name="whois_ip_3")    
    else:
        phantom.error("'whois_ip_3' will not be executed due to lack of parameters")
    
    return

def run_query_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'run_query_1' call
    filtered_results_data_1 = phantom.collect2(container=container, datapath=["ip_reputation_1:filtered-action_result.parameter.ip", "ip_reputation_1:filtered-action_result.parameter.context.artifact_id"], action_results=filtered_results)

    parameters = []
    
    # build parameters list for 'run_query_1' call
    for filtered_results_item_1 in filtered_results_data_1:
        if filtered_results_item_1[0]:
            parameters.append({
                'query': filtered_results_item_1[0],
                'display': "",
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': filtered_results_item_1[1]},
            })

    if parameters:
        phantom.act("run query", parameters=parameters, assets=['splunk_entr'], callback=join_Send_Email_bad_ip, name="run_query_1")    
    else:
        phantom.error("'run_query_1' will not be executed due to lack of parameters")
    
    return

def on_finish(container, summary):

    # This function is called after all actions are completed.
    # summary of all the action and/or all detals of actions 
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    return