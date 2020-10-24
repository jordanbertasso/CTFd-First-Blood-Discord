NAME = first-blood-bot

build:
	docker build -t jordanbertasso/$(NAME) .

stop:
	docker stop -t 0 $(NAME)

run:
	$(MAKE) stop; $(MAKE) build; docker run -d --rm --name $(NAME) jordanbertasso/$(NAME)

logs:
	docker logs -f $(NAME)
