from flasker import mqtt_client, topic

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)



@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
   data = dict(
       topic=message.topic,
       payload=message.payload.decode()
  )
   print('Received message on topic: {topic} with payload: {payload}'.format(**data))


# @app.route('/publish', methods=['POST'])
# def publish_message():
#    request_data = request.get_json()
#    publish_result = mqtt_client.publish(request_data['topic'], request_data['msg'])
#    return jsonify({'code': publish_result[0]})