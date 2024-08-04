class ModuleManager:
    def __init__(self):
        self.modules = []

    def add_module(self, module):
        self.modules.append(module)

    def remove_module(self, module):
        self.modules.remove(module)

    def run_all(self, img, **kwargs):
        for module in self.modules:
            if hasattr(module, 'run'):
                module.run(img, **kwargs)

    def draw_all(self, img):
        for module in self.modules:
            img = module.draw(img)
        return img

    def destroy_all(self):
        for module in self.modules:
            module.destroy()

    def get_modules_name(self):
        return [module.get_module_name() for module in self.modules]
