from unittest import TestCase

__author__ = 'mariosky'

from evospace import Individual, Population


class TestIndividual(TestCase):
    def setUp(self):
        self.population1 = Population("test_population1")
        self.population2 = Population("test_population2")

        self.population1.initialize()
        self.population2.initialize()


    def test_put(self):
        key = self.population1.individual_next_key()
        individual = Individual(id=key)
        individual.another_property = "test"
        self.assertEqual(individual.put(self.population1.name),True)
        self.assertEqual(individual.id,key)
        self.assertEqual(individual.another_property,"test")


    def test_get(self):
        key = self.population1.individual_next_key()
        individual = Individual(id=key)

        #No se puede hacer get sin guardar antes
        try:
            self.assertRaises(LookupError, individual.get())
        except:
            pass
        individual.put(self.population1.name)
        self.assertIsInstance(individual.get(),Individual)
        self.assertIsInstance(individual.get(as_dict=True),dict)


    def test_as_dict(self):
        key = self.population1.individual_next_key()
        individual = Individual(id=key)
        self.assertIsInstance(individual.as_dict(),dict)


    def test_two_populations(self):
        key = self.population1.individual_next_key()
        individual = Individual(id=key)
        individual.put(self.population1.name)
        individual.put(self.population2.name)
        self.assertIsInstance(individual.get(),Individual)
        self.assertIsInstance(individual.get(as_dict=True),dict)




