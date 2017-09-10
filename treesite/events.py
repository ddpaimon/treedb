import abc


class Event(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.next_event = None

    @abc.abstractmethod
    def serialize(self):
        """Serialize event to json format"""
        pass

    @abc.abstractmethod
    def apply(self, manager):
        """Apply event"""
        return None

    def set_next_event(self, event):
        self.next_event = event


class AddEvent(Event):
    def __init__(self, node_id, root, name):
        super(AddEvent, self).__init__()
        self.id = node_id
        self.root = root
        self.name = name

    def serialize(self):
        return {'name': "add", 'node_name': self.name, 'node_root': self.root, 'node_id': self.id}

    def apply(self, manager):
        print("Create new node with: name = " + self.name + " id = " + str(self.id) + " root = " + str(self.root))
        return 123


class DeleteEvent(Event):
    def __init__(self, node_id):
        super(DeleteEvent, self).__init__()
        self.id = node_id

    def serialize(self):
        return {'event_name': "delete", 'event_data': {'id': self.id}}

    def apply(self, manager):
        print("Delete node with: id = " + str(self.id))


class MoveEvent(Event):
    def __init__(self, node_id, root):
        super(MoveEvent, self).__init__()
        self.id = node_id
        self.root = root

    def serialize(self):
        return {'event_name': "move", 'event_data': {'id': self.id, 'root': self.root}}

    def apply(self, manager):
        print("Move node with: id = " + str(self.id))


class EventsManager:
    def __init__(self):
        self.last_event = self.first_event = None
        self.id_map = dict()

    def append_event(self, event):
        if self.last_event is None:
            self.last_event = self.first_event = event
        else:
            self.last_event.set_next_event(event)
            self.last_event = event

    def serialize_events(self):
        res = self._serialize_event(self.first_event)
        return res

    def _serialize_event(self, event):
        res = dict()
        if event is not None:
            res = event.serialize()
            res['next'] = self._serialize_event(event.next_event)
        return res

    def deserialize_event(self, event):
        if not bool(event):
            print("Events empty")
        else:
            concrete_event = None
            event_data = event['event_data']
            if event['event_name'] == "add":
                concrete_event = AddEvent(event_data['id'], event_data['root'], event_data['name'])
            elif event['event_name'] == "delete":
                concrete_event = DeleteEvent(event_data['id'])
            elif event['event_name'] == "move":
                concrete_event = MoveEvent(event_data['id'], event_data['root'])
            self.append_event(concrete_event)
            print(concrete_event.serialize())
            self.deserialize_event(event['event_next'])

    def apply(self):
        if self.last_event:
            self._apply(self.first_event)
        print(self.id_map)
        self.first_event = self.last_event = None
        self.id_map = dict()

    def _apply(self, event):
        node_id = event.apply(self)
        if node_id is not None:
            self.id_map[event.id] = node_id
        if event.next_event:
            self._apply(event.next_event)
