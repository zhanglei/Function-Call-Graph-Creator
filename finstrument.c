#include <stdio.h>

void __attribute__((__no_instrument_function__))
__cyg_profile_func_enter(void *this_func, void *call_site)
{
    FILE *fp = fopen("CallRecord.txt", "a");
    fprintf(fp, "Enter: %p,%p\n", this_func, call_site);
    fclose(fp);
}

void __attribute__((__no_instrument_function__))
__cyg_profile_func_exit(void *this_func, void *call_site)
{
    FILE *fp = fopen("CallRecord.txt", "a");
    fprintf(fp, "Leave: %p,%p\n", this_func, call_site);
    fclose(fp);
}
