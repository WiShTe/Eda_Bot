from .start import start_router
from .help import help_router
from .add_meal import add_meal_router
all_routers = [
    start_router,
    help_router,
    add_meal_router
]