from fastapi import FastAPI, Depends, Request

from storage.program.crud import ProgramsStorage


def get_programs_storage(request: Request) -> ProgramsStorage:
    pass
