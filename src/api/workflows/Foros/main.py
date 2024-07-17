from src.api.common.dependency_container_foros import DependencyContainer
import os


os.chdir('..')

DC = DependencyContainer(); DC.initialize()
DependencyContainer.get_foros_workflow().execute()