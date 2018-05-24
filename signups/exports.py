from csv import DictWriter


def export_participants_as_csv(participants, stream):
    fieldnames = [
        'first_name',
        'last_name',
        'email'
    ]
    writer = DictWriter(stream, fieldnames=fieldnames)
    writer.writer.writerow(['sep=,'])
    writer.writeheader()
    for participant in participants:
        writer.writerow({
            'first_name': participant.first_name,
            'last_name': participant.last_name,
            'email': participant.email
        })
    return stream
