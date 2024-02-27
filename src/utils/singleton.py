class Singleton(type):
    """Metaclass for creating singleton classes."""

    _instance = None

    def __call__(cls, *args, **kwargs):
        """Create a new instance of the singleton class.

        This method creates a new instance of the singleton class if one does not
        already exist. If an instance already exists, it will return the existing
        instance. This follows the singleton pattern.

        Returns
        -------
        Singleton
            The singleton instance of the class.
        """
        if cls not in cls._instance:
            instance = super().__call__(*args, **kwargs)
            cls._instance[cls] = instance
        return cls._instance[cls]
