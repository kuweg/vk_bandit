FROM python:3.9.13

WORKDIR /agents

COPY ../../agents/ /agents

COPY ../../configs/agent /agents/configs

RUN pip install --no-cache-dir --upgrade -r requirements_agent.txt

EXPOSE 8001

CMD ["python", "app.py", "ucb"]
