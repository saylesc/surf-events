FROM node:16 as surf-event-build

COPY frontend /usr/local/surfevents-capstone

WORKDIR /usr/local/surfevents-capstone

RUN npm install -g @angular/cli
RUN npm install
RUN ng build

# ENTRYPOINT [ "bash" ]
# ENTRYPOINT [ "ng", "serve" ]

######## Stage 2 #####
FROM nginx
COPY --from=surf-event-build /usr/local/surfevents-capstone/dist/frontend /usr/share/nginx/html

# docker run --name some-nginx -d -p 8080:80 some-content-nginx