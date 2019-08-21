#pragma once
struct node {
    int data;
    node *next;
    node(int num) :data(num), next(NULL) {}
};
