# -*- coding: utf-8 -*-
"""
SearchMetadata.py : Func6 - cercar imatges per metadades
Cada cerca retorna una llista d'UUID (pot ser buida).
"""


class SearchMetadata:

    def __init__(self, image_data):
        self.data = image_data

    def prompt(self, sub):
        return self.search(self.data.get_prompt, sub)

    def model(self, sub):
        return self.search(self.data.get_model, sub)

    def seed(self, sub):
        return self.search(self.data.get_seed, sub)

    def cfg_scale(self, sub):
        return self.search(self.data.get_cfg_scale, sub)

    def steps(self, sub):
        return self.search(self.data.get_steps, sub)

    def sampler(self, sub):
        return self.search(self.data.get_sampler, sub)

    def date(self, sub):
        return self.search(self.data.get_created_date, sub)

    def generated(self, sub):
        return self.search(self.data.get_generated, sub)

    def dimensions(self, width, height):
        # Si ens passen alguna cosa que no és un número, no pot coincidir cap imatge
        try:
            wanted = (int(width), int(height))
        except (ValueError, TypeError):
            return []

        result = []
        for uuid in self.data.get_uuids():
            if self.data.get_dimensions(uuid) == wanted:
                result.append(uuid)
        return result

    def and_operator(self, list1, list2):
        # Imatges que són a les dues llistes (en l'ordre de list1, sense repetir)
        in_list2 = set(list2)
        result = []
        for uuid in list1:
            if uuid in in_list2 and uuid not in result:
                result.append(uuid)
        return result

    def or_operator(self, list1, list2):
        # Imatges que són a una llista o a l'altra (sense repetir)
        result = []
        for uuid in list1 + list2:
            if uuid not in result:
                result.append(uuid)
        return result

    def search(self, get_field, sub):
        # Funció auxiliar: recorre totes les imatges i guarda les que contenen 'sub'
        # get_field és la funció que dóna el camp (get_prompt, get_model...)
        result = []
        for uuid in self.data.get_uuids():
            value = get_field(uuid)
            # Els camps buits ("None") i les imatges sense dades no compten
            if value is None or value == "None":
                continue
            if str(value).find(str(sub)) >= 0:
                result.append(uuid)
        return result

    def __str__(self):
        return "SearchMetadata: " + str(len(self.data)) + " imatges"