export enum ActionTypes{
    PAUSE = 'PAUSE',
    RESET = 'RESET',
    NEXT = 'NEXT',
}

export class Action {
    public constructor( public action: ActionTypes){};
}