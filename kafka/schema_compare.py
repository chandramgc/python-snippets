import json

def generate_kafka_schema_payload(subject, schema_definition):
    schema_payload = {
        "schema": json.dumps(schema_definition)
    }
    return json.loads(json.dumps(schema_payload))

def find_updated_fields(payload1, payload2):
    schema1 = json.loads(payload1['schema'])
    schema2 = json.loads(payload2['schema'])

    # Find the fields in schema2 that are missing or updated in schema1
    updated_fields = []
    for field2 in schema2['fields']:
        field1 = next((f for f in schema1['fields'] if f['name'] == field2['name']), None)
        if not field1 or field1['type'] != field2['type']:
            updated_fields.append(field2['name'])

    # Find the fields in schema1 that are missing in schema2
    missing_fields = []
    for field1 in schema1['fields']:
        field2 = next((f for f in schema2['fields'] if f['name'] == field1['name']), None)
        if not field2:
            missing_fields.append(field1['name'])

    return updated_fields, missing_fields

# Example usage
subject = "my-topic-value"
schema_definition1 = {
    "type": "record",
    "name": "User",
    "fields": [
        {"name": "name", "type": "string"},
        {"name": "age", "type": "int"},
        {"name": "dob", "type": "int"}
    ]
}
schema_definition2 = {
    "type": "record",
    "name": "User",
    "fields": [
        {"name": "name", "type": "string"},
        {"name": "age", "type": "long"},
        {"name": "city", "type": "string"}
    ]
}

payload1 = generate_kafka_schema_payload(subject, schema_definition1)
payload2 = generate_kafka_schema_payload(subject, schema_definition2)

updated_fields, missing_fields = find_updated_fields(payload1, payload2)
print("updated_fields : "+str(updated_fields))  # Output: ['age', 'city']
print("missing_fields : "+str(missing_fields))  # Output: []
