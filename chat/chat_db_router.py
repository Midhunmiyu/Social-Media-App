

class ChatDBRouter:
    """
    A database router to direct database operations for the chat app to 'chat_db'.
    """
    def db_for_read(self, model, **hints):
        """Direct read operations for chat models to 'chat_db'."""
        if model._meta.app_label == 'chat': #here chat is app name
            return 'chat_db'
        return None
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'chat':
            return 'chat_db'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'chat' or obj2._meta.app_label == 'chat':
            return True
        '''
         for allowing relation between chat and user 
        '''
        if (obj1._meta.app_label == 'chat' and obj2._meta.app_label == 'user') or \
           (obj1._meta.app_label == 'user' and obj2._meta.app_label == 'chat'):
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'chat':
            return db == 'chat_db'
        return None