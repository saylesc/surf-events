FROM node:16 as surf-event-build

COPY frontend /usr/local/surfevents-capstone

WORKDIR /usr/local/surfevents-capstone

RUN npm install -g @angular/cli
RUN npm install
RUN ng build

######## Stage 2 #####
FROM nginx
COPY --from=surf-event-build /usr/local/surfevents-capstone/dist/frontend /usr/share/nginx/html