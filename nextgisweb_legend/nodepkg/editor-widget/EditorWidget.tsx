import { observer } from "mobx-react-lite";

import { gettext } from "@nextgisweb/pyramid/i18n";
import type {
    EditorWidgetComponent,
    EditorWidgetProps,
} from "@nextgisweb/resource/type";

import type { EditorStore } from "./EditorStore";
import { FileLegendComponent } from "./component/FileLegendComponent";

import "./EditorWidget.less";

export const EditorWidget: EditorWidgetComponent<
    EditorWidgetProps<EditorStore>
> = observer(({ store }: EditorWidgetProps<EditorStore>) => {

    return (
        <div className="ngw-legend-editor-widget">
            <FileLegendComponent store={store} />
        </div>
    );
});

EditorWidget.title = gettext("Legend");
EditorWidget.activateOn = { create: true };
EditorWidget.order = -50;
