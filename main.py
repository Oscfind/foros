from src.api.common.dependency_container_foros import DependencyContainer

DC = DependencyContainer(); DC.initialize()
DependencyContainer.get_foros_workflow().execute()