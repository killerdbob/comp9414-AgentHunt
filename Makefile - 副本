
CC = gcc
CFLAGS = -Wall -03

CSRC = agent.c pipe.c
HSRC = pipe.h
OBJ = $(CSRC:.c=.o)

%o:%c $(HSRC)
	$(CC) $(CFLAGS) -c $<

.PHONY: clean

all:
	cp Agent.py agent
	chmod 755 agent

agent: $(OBJ)
	$(CC) -lm $(CFLAGS) -o agent $(OBJ)

clean:
	rm *.o *.class agent