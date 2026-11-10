NOVEL = novel
COUNT = 100

.PHONY: novel
novel:
	python generate.py "$(NOVEL)" -n "$(COUNT)"
