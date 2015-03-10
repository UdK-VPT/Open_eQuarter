class WidgetLinkedList:

    def __init__(self):
        self._head = None
        self._size = 0
        self.__current = self._head

    def __iter__(self):
        self.__current = self._head
        return self

    def next(self):
        if self.__current is None:
            raise StopIteration
        else:
            current = self.__current
            self.__current = self.__current.next
            return current

    def add_node(self, widget_node):
        if self._head is None:
            self._head = widget_node
        else:
            self._head.add_next(widget_node)

        self._size += 1

    def remove_node(self, widget_node):

        if self._head == widget_node:
            self._head =  self._head.next
            self._size -= 1

        else:
            previous = self._head
            current = previous.next

            while( current != widget_node ):
                previous = current
                current = previous.next

            if current == widget_node:
                previous.next = current.next
                self._size -= 1

    def get_node_at_position(self, position):

        for node_position, node in enumerate(self):
            if node_position == position:
                return node
        else:
            return None

    def get_index(self, node):

        for position, list_node in enumerate(self):
            if list_node == node:
                return position
        else:
            return -1

class WidgetLinkedListNode:

    def __init__(self):
        self.widgets = []
        self.next = None

    def add_widget(self, widget):
        self.widgets.append(widget)

    def remove_widget(self, widget):
        self.widgets.remove(widget)

    def add_next(self, widget_node):
        if self.next is None:
            self.next = widget_node
        else:
            self.next.add_next(widget_node)