def get_detail(self):
    self.object = self.get_object()
    self.object.read += 1
    self.object.save()
    context = self.get_context_data(object=self.object)
    return self.render_to_response(context)
