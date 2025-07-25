import cProfile
import pstats

cProfile.run("import AdvancementInterface", "profiler_result.txt")
stats = pstats.Stats("profiler_result.txt")
stats.sort_stats('time').print_stats(1000)
