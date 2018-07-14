
CC = gcc
CFLAGS = -Wall -03

CSRC = agent.c pipe.c
HSRC = pipe.h
OBJ = $(CSRC:.c=.o)

%o:%c $(HSRC)
	$(CC) $(CFLAGS) -c $<

.PHONY: clean

all:
	cp agent.py agent
	python3 Connectserver.py
	python3 evaluate.py
	python3 index_of_place.py
	python3 iworld.py
	python3 path.py
	python3 state.py
	chmod 755 agent

agent: $(OBJ)
	$(CC) -lm $(CFLAGS) -o agent $(OBJ)

clean:
	rm *.o *.class agent