# mylibrary
Basic django-celery app to manage physical library and keep track of to-read-list book prices. Goodreads like features can be added in future, such as shelves, reading activity and goodreads sync.

# Motivation
Manual Price checks takes lots of time and becames expired quickly. Automate that process by parsing supplier web sites periodically to monitor hundreds of books.

# Basic Installation
1. Make `docker`, `docker-compose` and `make` operable.
2. `cp .env.compose .env`
3. `make build`
4. `make up`
5. See all services running.

# Tests
Run `make test`.

# TODO
- [ ] Out of Stock conditions
- [ ] Periodic Price check
- [ ] Concurrent api calls
- [ ] Flags to report Price updates
- [ ] Admin registries
- [ ] Logger
