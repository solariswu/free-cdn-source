import yaml
import json
import os
import shutil
import json
import requests



BASE_DIR = '/mnt/efs'
BACKEND_YAML_TEMPLATE_FILENAME = 'openid_backend_template.yaml'
ROUTING_YAML_FILENAME = 'requester_based_routing.yaml'
PROXY_CONF_YAML_FILENAME = 'proxy_conf.yaml'
FRONTEND_YAML_FILENAME = 'saml2_frontend.yaml'
TENANTS_YAML_FILENAME = 'tenants.yaml'

PLUGIN_BASE_DIR = 'plugins/efs/'

# uses in multi-tenant only
# def create_backend_yaml(event):
#   with open(BASE_DIR+'/'+BACKEND_YAML_TEMPLATE_FILENAME, 'r') as f:
#     new_backend_yaml = yaml.safe_load(f)
#     f.close()

#   new_backend_yaml['name'] = event['tenantId'] + '_' + event['clientId']
#   new_backend_yaml['config']['provider_metadata']['issuer'] = event['issuer']
#   new_backend_yaml['config']['client']['client_metadata']['client_id'] = event['clientId']
#   new_backend_yaml['config']['client']['client_metadata']['client_secret'] = event['clientSecret']

#   with open(BASE_DIR+'/'+'backend_'+event['tenantId']+'_'+event['clientId']+'.yaml', 'w') as f:
#     yaml.dump(new_backend_yaml, f)
#     f.close()
      
#   with open(BASE_DIR+'/'+PROXY_CONF_YAML_FILENAME, 'r') as f:
#     proxy_conf_yaml = yaml.safe_load(f)
#     f.close()
    
#   print('proxy yaml backend type:', type(proxy_conf_yaml['BACKEND_MODULES']))
#   proxy_conf_yaml['BACKEND_MODULES'].append(PLUGIN_BASE_DIR+'backend_'+event['tenantId']+'_'+event['clientId']+'.yaml')

#   with open(BASE_DIR+'/'+PROXY_CONF_YAML_FILENAME, 'w') as f:
#     yaml.dump(proxy_conf_yaml, f)
#     f.close()
      
# def remove_backend_yaml(event):
#   os.remove(BASE_DIR+'/'+'backend_'+event['tenantId']+'_'+event['clientId']+'.yaml')
#   with open(BASE_DIR+'/'+PROXY_CONF_YAML_FILENAME, 'r') as f:
#     proxy_conf_yaml = yaml.safe_load(f)
#     f.close()
    
#   print('proxy yaml backend modules:', type(proxy_conf_yaml['BACKEND_MODULES']))
#   proxy_conf_yaml['BACKEND_MODULES'].remove(PLUGIN_BASE_DIR+'backend_'+event['tenantId']+'_'+event['clientId']+'.yaml')
  
#   with(BASE_DIR+'/'+PROXY_CONF_YAML_FILENAME, 'w') as f:
#     yaml.dump(proxy_conf_yaml, f)
#     f.close()

def add_sp_meta_url (event):
  with open(BASE_DIR+'/'+FRONTEND_YAML_FILENAME, 'r') as f:
    frontend_yaml = yaml.safe_load(f)
    f.close()
    
  frontend_yaml['config']['idp_config']['metadata']['remote'].append({'url': event['metadataUrl'], 'cert': None})
  
  with open(BASE_DIR+'/'+FRONTEND_YAML_FILENAME, 'w') as f:
    yaml.dump(frontend_yaml, f)
    f.close()
    
def add_tenant_routing (event):
  
  with open(BASE_DIR+'/'+ROUTING_YAML_FILENAME) as f:
     routing_yaml = yaml.safe_load(f)
     f.close()

  # multi-tenants backend code, backend is matching the samlproxy client id
  routing_yaml['config']['requester_mapping'][event['entityId']]=event['clientId']
  
  with open(BASE_DIR+'/'+ROUTING_YAML_FILENAME, "w") as f:
    yaml.dump(routing_yaml, f)
    f.close()

def remove_sp_meta_url (url):
  with open(BASE_DIR+'/'+FRONTEND_YAML_FILENAME, "r") as f:
    frontend_yaml = yaml.safe_load(f)
    f.close()
    
  frontend_yaml['config']['idp_config']['metadata']['remote'].remove({'url': url, 'cert': None})
  
  with open(BASE_DIR+'/'+FRONTEND_YAML_FILENAME, "w") as f:
    yaml.dump(frontend_yaml, f)
    f.close()
    
def remove_tenant_routing (entityId):
  with open(BASE_DIR+'/'+ROUTING_YAML_FILENAME) as f:
     routing_yaml = yaml.safe_load(f)
     f.close()

  removed = routing_yaml['config']['requester_mapping'].pop(entityId)

  with open(BASE_DIR+'/'+ROUTING_YAML_FILENAME, "w") as f:
    yaml.dump(routing_yaml, f)
    f.close()

def save_tenant_index (event):
  with open(BASE_DIR+'/'+TENANTS_YAML_FILENAME, 'r') as f:
    tenants_yaml = yaml.safe_load(f)
    f.close()
    
  tenants_yaml[event['entityId']+'_'+event['clientId']] = event
  
  with open(BASE_DIR+'/'+TENANTS_YAML_FILENAME, 'w') as f:
    yaml.dump(tenants_yaml, f)
    f.close()

def remove_tenant_index (entityId, clientId):
  with open(BASE_DIR+'/'+TENANTS_YAML_FILENAME, 'r') as f:
    tenants_yaml = yaml.safe_load(f)
    f.close()
    
  tenant = tenants_yaml.pop(entityId+'_'+clientId)
  
  with open(BASE_DIR+'/'+TENANTS_YAML_FILENAME, 'w') as f:
    yaml.dump(tenants_yaml, f)
    f.close()
    
  return tenant['metadataUrl']
  
def list_tenants ():
  tenants_yaml = {}
  #multi tenants - retrieve userpool info / tenant id / app client id info from token
  with open(BASE_DIR+'/'+TENANTS_YAML_FILENAME, 'r') as f:
    tenants_yaml = yaml.safe_load(f)
    f.close()
  
  
  # print ('tenant_yaml', tenant_yaml)
  return {
    'statusCode' : 200,
    'body': json.dumps(tenants_yaml)
  }

def create_tenant (event):
  add_sp_meta_url(event)
  # create_backend_yaml(event)
  add_tenant_routing(event)
  # download_sp_meta_file(payload)
  save_tenant_index(event)
  event['id'] = event['entityId']
  return event

def remove_tenant (entityId, clientId):
  url = remove_tenant_index(entityId, clientId)
  remove_tenant_routing(entityId)
  # remove_backend_yaml(event)
  remove_sp_meta_url(url)
  event['id'] = entityId
  return event
  
def get_tenant (id):
  with open(BASE_DIR+'/'+TENANTS_YAML_FILENAME, 'r') as f:
    tenants_yaml = yaml.safe_load(f)
    f.close()
    
  return tenants_yaml[id]

# def update_sp_meta_url (event):
#   with open(BASE_DIR+'/'+TENANTS_YAML_FILENAME) as f:
#     tenants_yaml = yaml.safe_load(f)
#     f.close()

#   sp_url = tenants_yaml[event['tenantId']]

#   with open(BASE_DIR+'/'+FRONTEND_YAML_FILENAME) as f:
#     frontend_yaml = yaml.safe_load(f)
#     f.close()

#   frontend_yaml['config']['idp_config']['metadata']['remote'].remove({'url': sp_url, 'cert': None})
#   frontend_yaml['config']['idp_config']['metadata']['remote'].append({'url': event['metadataUrl'], 'cert': None})

#   with open(BASE_DIR+'/'+FRONTEND_YAML_FILENAME, "w") as f:
#     yaml.dump(frontend_yaml, f)
#     f.close()
    
#   with open(BASE_DIR+'/'+TENANTS_YAML_FILENAME, "w") as f:
#     tenants_yaml[event['tenantId']] = event['metadataUrl']
#     yaml.dump(tenants_yaml, f)
#     f.close()
    
# def update_backend_yaml (event):
#   with open(BASE_DIR+'/'+BACKEND_YAML_TEMPLATE_FILENAME, 'r') as file:
#     new_backend_yaml = yaml.safe_load(file)
#     file.close()

#     new_backend_yaml['name'] = event['tenantId']
#     new_backend_yaml['config']['provider_metadata']['issuer'] = event['issuer']
#     new_backend_yaml['config']['client']['client_metadata']['client_id'] = event['clientId']
#     new_backend_yaml['config']['client']['client_metadata']['client_secret'] = event['clientSecret']

#     with open(BASE_DIR+'/'+'backend_'+event['tenantId']+'.yaml', 'w') as file:
#       yaml.dump(new_backend_yaml, file)
#       file.close()
      
# def update_tenant_routing (event)
#   with open(BASE_DIR+'/'+ROUTING_YAML_FILENAME, "r") as f:
#     routing_yaml = yaml.safe_load(f)
#     f.close()

#     with routing_yaml['config']['requester_mapping'] as rmapping:
#       items = {k: v for k, v in rmapping.items() if v != event['tenantId']}
#       items[event['entityId']] = event['tenantId']
#       routing_yaml['config']['requester_mapping']=items
  
#   with open(BASE_DIR+'/'+ROUTING_YAML_FILENAME, "w") as f:
#     yaml.dump(routing_yaml, f)
#     f.close()



# def download_sp_meta_file (event):
#   response = requests.get(event['url'], stream=True)
  
#   with open(BASE_DIR+'/'+'sample.json', 'wb') as out_file:
#     shutil.copyfileobj(response.raw, out_file)

def lambda_handler(event, context):

  print('ygwu event', event)
  print('ygwu context', context)

  method = event['requestContext']['http']['method']
  result = {
    'statusCode': 400,
    'body': json.dumps({'data': 'Bad request'})
  }
  if method == 'POST':
    payload = json.loads(event['body'])
    result = create_tenant(payload)
  elif method == 'DELETE' and event.get('pathParameters') is not None:
    payload = json.loads(event['body'])
    result = remove_tenant(event['pathParameters']['id'], payload['clientId'])
  elif method == 'PUT':
    update_tenant_routing(event)
    result = update_backend_yaml(event)
  elif method == 'GET':
    if event.get('pathParameters') is not None:
      result = get_tenant(event['pathParameters']['id'])
    else :
      result = list_tenants()
      
  return result


