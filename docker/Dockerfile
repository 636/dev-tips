FROM

LABEL version=1.0

ENV USER_NAME=master
ENV HOME=/home/master
RUN echo "${USER_NAME} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/${USER_NAME}
RUN chmod u+s /usr/sbin/useradd && chmod u+s /usr/sbin/groupadd

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]